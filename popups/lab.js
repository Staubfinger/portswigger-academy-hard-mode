function submithint() {
    console.log(`Submitting Hint request with ${document.getElementById('cat').value}`)
    browser.runtime.sendMessage({
        type: 'hint',
        hint: document.getElementById('cat').value
    });
}

function reset() {
    browser.browserAction.setPopup({
        popup: browser.runtime.getURL('popups/popup.html')
    })
    window.close()
}

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('hint')) {
        submithint()
    } else if (e.target.classList.contains('reset')) {
        reset()
    }

});
