const vscode = require("vscode");
const { execFile } = require("child_process");
const path = require("path");

function activate(context) {
    console.log("Strand extension activated");

    // Command for validating DNA or FASTA files
    let validateCommand = vscode.commands.registerCommand(
        "strand.validate",
        function () {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;

            const document = editor.document;
            const text = document.getText();
            const lines = text.split("\n");

            let isValid = true;
            lines.forEach((line, index) => {
                if (index === 0 && !line.startsWith(">")) {
                    vscode.window.showErrorMessage(
                        `Invalid FASTA file: First line must start with ">".`
                    );
                    isValid = false;
                } else if (index > 0 && !/^[ACTG\s]*$/i.test(line)) {
                    vscode.window.showErrorMessage(
                        `Invalid DNA sequence on line ${index + 1}: Only A, C, T, G are allowed.`
                    );
                    isValid = false;
                }
            });

            if (isValid) {
                vscode.window.showInformationMessage("FASTA file is valid!");
            }
        }
    );

    // Command for visualizing pathways
    let visualizeCommand = vscode.commands.registerCommand(
        "strand.visualize",
        function () {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showErrorMessage("No active editor found.");
                return;
            }

            const document = editor.document;
            const dnaSequence = document.getText();

            // Path to the Python interpreter script
            const pythonInterpreter = path.join(__dirname, "../interpreter.py");

            // Call the Python interpreter
            execFile("python3", [pythonInterpreter, dnaSequence], (error, stdout, stderr) => {
                if (error) {
                    vscode.window.showErrorMessage(`Error interpreting DNA: ${stderr}`);
                    return;
                }

                try {
                    const results = JSON.parse(stdout); // Ensure the Python script returns JSON
                    const { Proteins, Environment, Viruses } = results;

                    const graphNodes = [];
                    const graphEdges = [];

                    // Add nodes and edges for proteins
                    Proteins.forEach((protein, index) => {
                        graphNodes.push({ id: `Protein_${index}`, label: protein });
                        if (index > 0) {
                            graphEdges.push({
                                source: `Protein_${index - 1}`,
                                target: `Protein_${index}`,
                            });
                        }
                    });

                    // Add nodes for environment variables
                    Object.keys(Environment).forEach((key) => {
                        graphNodes.push({ id: `Env_${key}`, label: `${key}: ${Environment[key]}` });
                        graphEdges.push({
                            source: `Env_${key}`,
                            target: `Protein_0`, // Connect environment to the first protein
                        });
                    });

                    // Add nodes and edges for viruses
                    Viruses.forEach((virus, index) => {
                        graphNodes.push({ id: `Virus_${index}`, label: virus });
                        graphEdges.push({
                            source: `Virus_${index}`,
                            target: `Protein_0`, // Assume viruses affect the first protein
                        });
                    });

                    // Create a webview and render the graph
                    const panel = vscode.window.createWebviewPanel(
                        "strandVisualizer",
                        "Strand Pathway Visualizer",
                        vscode.ViewColumn.One,
                        { enableScripts: true }
                    );

                    panel.webview.html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Strand Visualizer</title>
    <script src="https://unpkg.com/cytoscape/dist/cytoscape.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
        }
        h1 {
            color: #007acc;
            text-align: center;
        }
        #graph {
            width: 100%;
            height: 600px;
            margin: 20px auto;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <h1>Strand Pathway Visualization</h1>
    <div id="graph"></div>
    <script>
        const cy = cytoscape({
            container: document.getElementById('graph'),
            elements: [
                ${graphNodes.map(
                    (node) => `{ data: { id: "${node.id}", label: "${node.label}" } }`
                ).join(",")},
                ${graphEdges.map(
                    (edge) =>
                        `{ data: { source: "${edge.source}", target: "${edge.target}" } }`
                ).join(",")}
            ],
            style: [
                {
                    selector: "node",
                    style: {
                        "background-color": "#007acc",
                        "label": "data(label)",
                        "text-valign": "center",
                        "color": "#fff",
                        "width": 20,
                        "height": 20,
                        "font-size": "10px",
                    }
                },
                {
                    selector: "edge",
                    style: {
                        "width": 2,
                        "line-color": "#ccc",
                        "target-arrow-color": "#ccc",
                        "target-arrow-shape": "triangle",
                    }
                }
            ],
            layout: {
                name: "breadthfirst",
                directed: true,
                padding: 10,
            }
        });
    </script>
</body>
</html>`;
                } catch (err) {
                    vscode.window.showErrorMessage(
                        `Error processing results: ${err.message}`
                    );
                }
            });
        }
    ); 

    context.subscriptions.push(validateCommand, visualizeCommand);
}

function getWebviewContent(proteins, environment, graphData, edges) {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strand Visualizer</title>
    <script src="https://unpkg.com/cytoscape/dist/cytoscape.min.js"></script>
    <style>
        #cy {
            width: 100%;
            height: 400px;
            border: 1px solid #ccc;
        }
        body {
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    <h1>Strand Pathway Visualization</h1>
    <div id="cy"></div>
    <h2>Proteins</h2>
    <p>${proteins.join(", ")}</p>
    <h2>Environment</h2>
    <pre>${JSON.stringify(environment, null, 2)}</pre>
    <script>
        const cy = cytoscape({
            container: document.getElementById('cy'),
            elements: [
                ${graphData
                    .map(node => `{ data: { id: "${node.id}", label: "${node.label}" } }`)
                    .join(",")},
                ${edges
                    .map(edge => `{ data: { source: "${edge.from}", target: "${edge.to}" } }`)
                    .join(",")}
            ],
            style: [
                {
                    selector: "node",
                    style: {
                        "background-color": "#007acc",
                        "label": "data(label)"
                    }
                },
                {
                    selector: "edge",
                    style: {
                        "width": 2,
                        "line-color": "#ccc"
                    }
                }
            ],
            layout: {
                name: "breadthfirst"
            }
        });
    </script>
</body>
</html>
`;
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};