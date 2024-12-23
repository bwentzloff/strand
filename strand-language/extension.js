const vscode = require('vscode');
const graphviz = require('d3-graphviz');

function activate(context) {
    let disposable = vscode.commands.registerCommand('strand.visualize', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found.');
            return;
        }

        const document = editor.document;
        const dnaContent = document.getText();

        try {
            const jsonOutput = JSON.parse(dnaContent);

            const relevantTicks = jsonOutput.filter(tickData => tickData.State);
            const visualization = relevantTicks.map(tick => {
                return `Tick ${tick.Tick}: ${JSON.stringify(tick.State, null, 2)}`;
            }).join("\n\n");

            vscode.window.showInformationMessage(`Visualization:\n${visualization}`);
        } catch (error) {
            vscode.window.showErrorMessage('Error processing DNA: Invalid JSON.');
        }
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
