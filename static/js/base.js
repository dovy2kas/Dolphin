function closeToast() {

    try{
        document.getElementById("toast-danger").style.display = "none";
    } catch (e) {
    }

    try{
        document.getElementById("toast-success").style.display = "none";
    } catch (e) {
    }
    
}