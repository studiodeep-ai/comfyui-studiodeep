import { app } from "../../scripts/app.js";

let INGREDIENTS_DATA = {};

// Fetch all ingredient data once at load time
fetch("/studiodeep/prompt_ingredients")
    .then(r => r.json())
    .then(data => { INGREDIENTS_DATA = data; })
    .catch(() => {});

function applyIngredientOptions(node, typeLabel) {
    const ingredientWidget = node.widgets?.find(w => w.name === "ingredient");
    if (!ingredientWidget) return;

    const typeData = INGREDIENTS_DATA[typeLabel];
    const titles = typeData?.ingredients?.map(i => i.title) ?? [];

    ingredientWidget.options.values = titles.length ? titles : ["(none)"];

    if (!titles.includes(ingredientWidget.value)) {
        ingredientWidget.value = titles[0] ?? "(none)";
    }
}

app.registerExtension({
    name: "StudioDeep.PromptIngredient",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "SD_PromptIngredient") return;

        const origOnConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function (data) {
            origOnConfigure?.apply(this, arguments);

            const typeWidget = this.widgets?.find(w => w.name === "ingredient_type");
            if (!typeWidget) return;

            applyIngredientOptions(this, typeWidget.value);

            const origCallback = typeWidget.callback;
            typeWidget.callback = (value) => {
                origCallback?.call(this, value);
                applyIngredientOptions(this, value);
            };
        };
    },

    async nodeCreated(node) {
        if (node.comfyClass !== "SD_PromptIngredient") return;

        const typeWidget = node.widgets?.find(w => w.name === "ingredient_type");
        if (!typeWidget) return;

        applyIngredientOptions(node, typeWidget.value);

        const origCallback = typeWidget.callback;
        typeWidget.callback = (value) => {
            origCallback?.call(node, value);
            applyIngredientOptions(node, value);
        };

        node.addWidget("button", "↺ Refresh", null, async () => {
            const resp = await fetch("/studiodeep/prompt_ingredients/reload", { method: "POST" });
            INGREDIENTS_DATA = await resp.json();

            // Update ingredient_type options in case new JSON files were added
            const labels = Object.keys(INGREDIENTS_DATA);
            typeWidget.options.values = labels.length ? labels : ["(none)"];
            if (!labels.includes(typeWidget.value)) {
                typeWidget.value = labels[0] ?? "(none)";
            }

            applyIngredientOptions(node, typeWidget.value);
            node.setDirtyCanvas(true, true);
        });
    },
});
