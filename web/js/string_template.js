import { app } from "../../scripts/app.js";

function syncInputs(node, template) {
    const regex = /\{\{(var\d+)\}\}/g;
    const found = [];
    let m;
    while ((m = regex.exec(template)) !== null) {
        if (!found.includes(m[1])) found.push(m[1]);
    }

    // Skip all DOM work if the input slots already match exactly
    const current = node.inputs.map(inp => inp.name);
    if (current.length === found.length && current.every((n, i) => n === found[i])) return;

    // Remove input slots no longer present in the template
    for (let i = node.inputs.length - 1; i >= 0; i--) {
        if (!found.includes(node.inputs[i].name)) {
            node.removeInput(i);
        }
    }

    // Add slots for new variables, preserving order
    const existing = node.inputs.map(inp => inp.name);
    for (const varName of found) {
        if (!existing.includes(varName)) {
            node.addInput(varName, "STRING");
        }
    }

    node.setDirtyCanvas(true, true);
}

function attachTemplateWidget(node) {
    const templateWidget = node.widgets?.find(w => w.name === "template");
    if (!templateWidget) return;

    syncInputs(node, templateWidget.value);

    // Guard against re-attaching listeners if called more than once
    if (node._sdTemplateListenerAttached) return;
    node._sdTemplateListenerAttached = true;

    const origCallback = templateWidget.callback;
    templateWidget.callback = function (value) {
        origCallback?.apply(this, arguments);
        syncInputs(node, value);
    };

    if (templateWidget.inputEl) {
        templateWidget.inputEl.addEventListener("input", () => {
            syncInputs(node, templateWidget.inputEl.value);
        });
    }
}

app.registerExtension({
    name: "StudioDeep.StringTemplate",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "SD_StringTemplate") return;

        const origOnConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function (data) {
            origOnConfigure?.apply(this, arguments);
            attachTemplateWidget(this);
        };
    },

    async nodeCreated(node) {
        if (node.comfyClass !== "SD_StringTemplate") return;
        attachTemplateWidget(node);
    },
});
