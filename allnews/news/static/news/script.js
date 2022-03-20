let times = 60

function load_page() {
    document.querySelector('select').value = times
    setTimeout(function() { window.location.reload(); }, parseInt(times)*1000);
}

function get_refresh_time() {
        times = document.querySelector('select').value
    }


window.onload = load_page