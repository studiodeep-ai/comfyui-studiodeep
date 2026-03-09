import { app } from "../../scripts/app.js";

const CLAUDE_MODELS = [
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "claude-haiku-4-5-20251001",
];

const OPENAI_MODELS = [
    "gpt-5o",
    "gpt-5o-mini",
];

const PROVIDER_MODELS = {
    Claude: CLAUDE_MODELS,
    OpenAI: OPENAI_MODELS,
};

function applyProviderModels(node, provider) {
    const modelWidget = node.widgets?.find(w => w.name === "model");
    if (!modelWidget) return;

    const models = PROVIDER_MODELS[provider];
    if (!models) return;

    modelWidget.options.values = models;

    // Reset to first model of provider if current selection doesn't belong to it
    if (!models.includes(modelWidget.value)) {
        modelWidget.value = models[0];
    }
}

app.registerExtension({
    name: "StudioDeep.LLMBackend",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "SD_LLMBackend") return;

        const origOnConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function (data) {
            origOnConfigure?.apply(this, arguments);

            const providerWidget = this.widgets?.find(w => w.name === "provider");
            if (!providerWidget) return;

            // Apply correct model list for the saved provider on load
            applyProviderModels(this, providerWidget.value);

            // Watch for provider changes
            const origCallback = providerWidget.callback;
            providerWidget.callback = (value) => {
                origCallback?.call(this, value);
                applyProviderModels(this, value);
            };
        };
    },

    async nodeCreated(node) {
        if (node.comfyClass !== "SD_LLMBackend") return;

        const providerWidget = node.widgets?.find(w => w.name === "provider");
        if (!providerWidget) return;

        applyProviderModels(node, providerWidget.value);

        const origCallback = providerWidget.callback;
        providerWidget.callback = (value) => {
            origCallback?.call(node, value);
            applyProviderModels(node, value);
        };
    },
});
