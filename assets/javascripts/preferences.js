/*
 * Licence MIT - Copyright (c) 2023 Kamil Krzyśków (HRY)
 */

const gmcPreferenceHandler = (event) => {
    console.debug(event);
    const target = event.target;
    const option = target.dataset["option"];
    // preferencesKey defined in extrahead template override
    let loadedPreferences = __md_get(preferencesKey);

    if (option === "color") {
        let prev = loadedPreferences["color"];
        if (!prev) {
            loadedPreferences["color"] = {};
            loadedPreferences["__global"] = {};
        }

        // TODO Separate raw css builder from value assignment, perhaps it's time for OOP...
        // TODO Implement some HEX to HSL conversion logic
        // https://stackoverflow.com/questions/3732046/how-do-you-get-the-hue-of-a-xxxxxx-colour

        loadedPreferences["color"]["value"] = target.value;
        loadedPreferences["__global"]["cssRaw"] = `* { --md-typeset-a-color: ${target.value}!important; }
        [data-md-color-scheme="slate"] .md-header { border-bottom: .10rem solid ${target.value}; }
        [data-md-color-scheme="slate"] .md-tabs { background-color: ${target.value} !important; }`;
    }

    __md_set(preferencesKey, loadedPreferences)
    // Function defined in extrahead template override
    gmcLoadSetPreferences();
};

/**
 * Removes the translation prompts from the page.
 * Mostly a quick hack for the GMC Preferences page.
 * Once this function is used more than 3 times,
 * it would be better to have a backend preprocessor solution.
 */
const removeRedundantTranslationIndicator = () => {
    const itemsToRemove = [
        document.querySelector("#gmc-new-translation-button"),
        document.querySelector(".gmc-announce")
    ];

    for (const item of itemsToRemove) {
        console.debug(item)
        if (item) {
            item.remove();
        }
    }
};

/*
    This is run immediately when loaded to add the elements before the bundle.js
    overrides the title tooltip logic. DOMContentLoaded is too late.
*/
(() => {

    // Defined in extrahead template override
    gGMC_REMOVE_TRANSLATION_PROMPTS = true;
    removeRedundantTranslationIndicator();

    let lastElement = document.querySelector("#preferences-start");
    const localizationElement = document.querySelector("#preferences-config-localization");

    if (!lastElement || !localizationElement) {
        console.debug("Preferences management couldn't find specified elements");
        return;
    }

    // TODO export into a separate function to keep localization gathering disconnected from rendering
    const localizationMatrix = JSON.parse(localizationElement.textContent);
    let currentLocalization = localizationMatrix["en"];
    const langCode = location.pathname.split("/")[2];
    const langCodeLocalization = localizationMatrix[langCode];

    if (langCodeLocalization) {
        currentLocalization = {...currentLocalization, ...langCodeLocalization}
    }

    console.debug(lastElement)
    console.debug(localizationMatrix)
    console.debug(langCode)
    console.debug(langCodeLocalization)
    console.debug(currentLocalization)

    const h1Tag = document.querySelector(".md-content h1");
    if (h1Tag) {
        h1Tag.childNodes[0].nodeValue = currentLocalization["h1Content"];
    }
    lastElement.innerText = currentLocalization["firstParagraph"];

    const optionNames = ["color", "headingShadow"];

    for (let option of optionNames) {
        if (option !== "color") {
            console.debug("for now only color works")
            break;
        }

        console.debug(option)

        const title = document.createElement("h2");
        title.innerText = currentLocalization[`${option}Title`];
        lastElement.insertAdjacentElement("afterend", title);

        const description = document.createElement("p");
        description.innerText = currentLocalization[`${option}Description`];
        title.insertAdjacentElement("afterend", description);

        const inputWrapper = document.createElement("p");
        const input = document.createElement("input");
        input.type = "text";
        if (option === "color") {
            input.type = option;
        }
        input.dataset["option"] = option;
        input.title = option;
        if (option !== "color") {
            input.className = "md-input";
        }
        input.addEventListener("change", gmcPreferenceHandler);
        inputWrapper.appendChild(input);
        description.insertAdjacentElement("afterend", inputWrapper);

        lastElement = inputWrapper;
    }
})();