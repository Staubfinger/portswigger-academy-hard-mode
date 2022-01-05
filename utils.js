// Just some utility functions, in case new categories are being added

// TODO  add code to auto-gen categories, rip out of background.js
var categories = []

function getName(string){
    // want to do meow-catz into Meow Catz
    string = string.replace(/-([a-z])/g, function (g) { return " " + g[1].toUpperCase(); });
    return string[0].toUpperCase() + string.substring(1)
}

categories.forEach(curr => {
    Options_HTML = `<option value="${curr}">${getName(curr)}</option>`
    HTMLString += Options_HTML
});

console.log(HTMLString)

