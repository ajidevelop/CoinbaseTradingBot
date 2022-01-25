const { app, BrowserWindow, ipcMain, ipcRenderer } = require('electron')
const { CoinbaseAuth } = require('./app/auth.js')
const { StopLossTakeProfit } = require('./app/webhooks')

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
  })

  win.loadFile('index.html')
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})
