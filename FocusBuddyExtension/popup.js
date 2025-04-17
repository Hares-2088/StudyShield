// Load blocked sites from storage
let blockedSites = [];
chrome.storage.sync.get(['blockedSites'], function (data) {
  if (data.blockedSites) {
    blockedSites = data.blockedSites;
    updateSiteList();
  }
});

// Add a website to the blocklist
document.getElementById('add-site').addEventListener('click', () => {
  const siteInput = document.getElementById('site-input');
  const site = siteInput.value.trim();
  if (site && !blockedSites.includes(site)) {
    blockedSites.push(site);
    chrome.storage.sync.set({ blockedSites }, () => {
      updateSiteList();
      siteInput.value = '';
    });
  }
});

// Update the list of blocked sites
function updateSiteList() {
  const siteList = document.getElementById('site-list');
  siteList.innerHTML = '';
  blockedSites.forEach(site => {
    const li = document.createElement('li');
    li.textContent = site;
    siteList.appendChild(li);
  });
}

// Start focus session
document.getElementById('start-focus').addEventListener('click', () => {
  chrome.runtime.sendMessage({ action: 'startFocus', blockedSites });
  window.close(); // Close the popup
});