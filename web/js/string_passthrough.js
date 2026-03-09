import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "StudioDeep.StringPassthrough",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "SD_StringPassthrough") return;

        // Restore read-only state when a saved workflow is loaded
        const origOnConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function (data) {
            origOnConfigure?.apply(this, arguments);
            setReadOnly(this);
        };

        // Update the preview widget when the node finishes executing
        nodeType.prototype.onExecuted = function (data) {
            const previewWidget = this.widgets?.find(w => w.name === "preview");
            if (previewWidget && data?.text?.length) {
                previewWidget.value = data.text[0];
                this.setDirtyCanvas(true);
            }
        };
    },

    async nodeCreated(node) {
        if (node.comfyClass !== "SD_StringPassthrough") return;
        setReadOnly(node);
    },
});

function setReadOnly(node) {
    const previewWidget = node.widgets?.find(w => w.name === "preview");
    if (previewWidget?.inputEl) {
        previewWidget.inputEl.readOnly = true;
        previewWidget.inputEl.style.opacity = "0.75";
        previewWidget.inputEl.style.cursor = "default";
    }
}
