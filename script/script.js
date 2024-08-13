document.querySelectorAll('.folder-name').forEach(folderName => {
    folderName.addEventListener('click', () => {
        const folder = folderName.parentElement;
        folder.classList.toggle('open');
    });
});
