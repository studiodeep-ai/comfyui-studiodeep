import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "StudioDeep.JSONShotSplitter",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "SD_JSONShotSplitter") return;

        // Restore correct output count when a saved workflow is loaded
        const origOnConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function (data) {
            origOnConfigure?.apply(this, arguments);
            const countWidget = this.widgets?.find(w => w.name === "shot_count");
            if (countWidget) syncOutputs(this, countWidget.value);
        };
    },

    async nodeCreated(node) {
        if (node.comfyClass !== "SD_JSONShotSplitter") return;

        const countWidget = node.widgets?.find(w => w.name === "shot_count");
        if (!countWidget) return;

        // Trim the 20 slots Python registered down to shot_count immediately
        syncOutputs(node, countWidget.value);

        // Watch widget changes and sync output slots
        const origCb = countWidget.callback;
        countWidget.callback = function (value) {
            origCb?.apply(this, arguments);
            syncOutputs(node, value);
        };
    },
});

function syncOutputs(node, count) {
    count = Math.max(1, Math.min(Math.floor(count), 20));
    const current = node.outputs.length;

    if (current < count) {
        for (let i = current; i < count; i++) {
            node.addOutput(`shot_${i + 1}`, "STRING");
        }
    } else if (current > count) {
        for (let i = current - 1; i >= count; i--) {
            node.removeOutput(i);
        }
    }

    node.setDirtyCanvas(true, true);
}
