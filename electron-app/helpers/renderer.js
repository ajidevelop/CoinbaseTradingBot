window.api.receive("fromMain", (data) => {
	console.log(`Received ${data} from main process`);
});

document.getElementById('coin-form').addEventListener('submit', (event) => {
	console.log('test')

	event.preventDefault();
	let coin1 = document.getElementById('coin-one').value.toUpperCase()
	let coin2 = document.getElementById('coin-two').value.toUpperCase()
	let coin_pair = `${coin1}-${coin2}`
	let entry = document.getElementById('stop_loss').value
	let exit = document.getElementById('exit').value
	let data = {
		'product_id': coin_pair,
		'sltp': {
			'stop_loss': entry,
			'take_profit': {
				1: exit
			}
		}
	}
	window.api.send('toMain', data);
})

