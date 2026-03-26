import { app } from "../../scripts/app.js";

let DESCRIBERS_DATA = {};

// Fetch all describer data once at load time
fetch("/studiodeep/describers")
    .then(r => r.json())
    .then(data => { DESCRIBERS_DATA = data; })
    .catch(() => {});

app.registerExtension({
    name: "StudioDeep.Describer",

    async nodeCreated(node) {
        if (node.comfyClass !== "SD_Describer") return;

        const describerWidget = node.widgets?.find(w => w.name === "describer");
        if (!describerWidget) return;

        // Populate dropdown from loaded data
        const labels = Object.keys(DESCRIBERS_DATA);
        if (labels.length) {
            describerWidget.options.values = labels;
            if (!labels.includes(describerWidget.value)) {
                describerWidget.value = labels[0];
            }
        }

        node.addWidget("button", "↺ Refresh", null, async () => {
            const resp = await fetch("/studiodeep/describers/reload", { method: "POST" });
            DESCRIBERS_DATA = await resp.json();

            const updatedLabels = Object.keys(DESCRIBERS_DATA);
            describerWidget.options.values = updatedLabels.length ? updatedLabels : ["(none)"];
            if (!updatedLabels.includes(describerWidget.value)) {
                describerWidget.value = updatedLabels[0] ?? "(none)";
            }

            node.setDirtyCanvas(true, true);
        });
    },
});
