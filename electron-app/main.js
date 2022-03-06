const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path');
const service = require('./helpers/service')

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "/helpers/preload.js")
    }
  })

  win.loadFile('index.html')
}

app.whenReady().then(() => {
  createWindow()


  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

ipcMain.on('toMain', (event, arg) => {
  service.newCoinPair(arg)
})