const { app, BrowserWindow, ipcMain, ipcRenderer } = require('electron')
const path = require('path');

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js")
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

ipcMain.on('coin-info', (event, arg) => {
  console.log(arg)
}).on('toMain', (event, arg) => {
  console.log(arg)
})