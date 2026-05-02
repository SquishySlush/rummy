document.addEventListener("DOMContentLoaded", () => {
    const search = document.querySelector("input[name='Rules'], .top-search input");
    search?.addEventListener("input", filterRules);

    const buttons = [...document.querySelectorAll("button")];
    const importButton = buttons.find((button) => button.textContent.toLowerCase().includes("import"));
    const exportButton = buttons.find((button) => button.textContent.toLowerCase().includes("export"));

    importButton?.addEventListener("click", importRules);
    exportButton?.addEventListener("click", exportRules);
});

function filterRules() {
    const query = (document.querySelector("input[name='Rules'], .top-search input")?.value || "").trim().toLowerCase();
    document.querySelectorAll(".scroll-list > *").forEach((row) => {
        row.style.display = row.textContent.toLowerCase().includes(query) ? "" : "none";
    });
}

function collectRules() {
    const rules = {};
    document.querySelectorAll(".scroll-list [name]").forEach((control) => {
        if (!control.name) return;
        if (control.type === "checkbox") rules[control.name] = control.checked;
        else if (control.type === "number") rules[control.name] = control.value === "" ? null : Number(control.value);
        else if (control.name === "wilds") rules[control.name] = parseWilds(control.value);
        else rules[control.name] = control.value;
    });
    return rules;
}

function applyRules(rules) {
    document.querySelectorAll(".scroll-list [name]").forEach((control) => {
        if (!control.name || !(control.name in rules)) return;
        const value = rules[control.name];
        if (control.type === "checkbox") control.checked = Boolean(value);
        else if (control.name === "wilds") control.value = formatWilds(value);
        else control.value = value ?? "";
    });
}

function exportRules() {
    const blob = new Blob([JSON.stringify(collectRules(), null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "ruleset.json";
    link.click();
    URL.revokeObjectURL(url);
}

function importRules() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "application/json";
    input.addEventListener("change", () => {
        const file = input.files?.[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
            try { applyRules(JSON.parse(reader.result)); }
            catch { alert("Invalid JSON file"); }
        };
        reader.readAsText(file);
    });
    input.click();
}

function parseWilds(value) {
    if (!value?.trim()) return [];
    return value.split(",").map((item) => item.trim()).filter(Boolean).map((item) => {
        const [rank, count] = item.split(":");
        return [rank.trim(), Number(count || 0)];
    });
}

function formatWilds(wilds) {
    if (!Array.isArray(wilds)) return "";
    return wilds.map((item) => Array.isArray(item) ? `${item[0]}:${item[1]}` : "").filter(Boolean).join(", ");
}
