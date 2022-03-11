const axios  = require('axios')

axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.headers.post['Content-Type'] = 'application/json'
function newCoinPair(data) {
	console.log(data)
	axios.post('new_order', {data: data}).then(r  => {
	})
 }

module.exports = {
	newCoinPair
}