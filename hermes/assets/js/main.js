function initTabs() {
    function initHashNavigation() {
        const hash = location.hash.replace(/^#/, '')
        if (hash) {
            const tabElement = document.querySelector('.nav-tabs [data-mdb-target="#' + hash + '"]')
            tabElement.click()
        }
    }

    function initUpdateUrlHashOnNavigation() {
        document.querySelectorAll('.nav-tabs button').forEach(function (nav) {
            nav.addEventListener('click', function (e) {
                location.hash = e.target.dataset['mdb-target']
            })
        })
    }

    initHashNavigation();
    initUpdateUrlHashOnNavigation();
}

function initCopyToClipboard() {
    function copyText(text) {
        const errorText = '\'Your browser does not supported copying to the clipboard\''
        if (!navigator.clipboard) {
            alert(errorText)

            return
        }

        navigator.clipboard.writeText(text)
            .catch(function (e) {
                alert(errorText)
                console.error(e)
            });
    }

    document.querySelectorAll('.copy').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const textElement = document.querySelector(e.target.dataset['copy-target'])
            const text = textElement.value || textElement.textContent || textElement.innerText;

            copyText(text)
        })
    })
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('🌬 📧 📬');

    initTabs();
    initCopyToClipboard();
});