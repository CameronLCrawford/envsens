<script>

	// Imports
	import { onMount } from 'svelte';
	import { Line } from 'svelte-chartjs';
	import 'chartjs-adapter-date-fns';
	import {
		Chart as ChartJS,
		Title,
		Tooltip,
		Legend,
		LineElement,
		LinearScale,
		PointElement,
		CategoryScale,
		TimeScale
	} from 'chart.js';
	ChartJS.register(
		Title,
		Tooltip,
		Legend,
		LineElement,
		LinearScale,
		PointElement,
		CategoryScale,
		TimeScale
	);
	const lineOptions = {
		responsive: true,
		maintainAspectRatio: false,
		scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second'
                }
            }
        }
	};

	// Each of these is fetched from API
	let currentTemp;
	let pastHour;
	let data;

	onMount(async () => {
		const mostRecentResponse = await fetch(
			'http://envsens.local:8081/temp/most-recent', {
				method: 'GET'
			}
		);
		currentTemp = await mostRecentResponse.json();

		const pastHourResponse = await fetch(
			'http://envsens.local:8081/temp/past-hour', {
				method: 'GET'
			}
		);
		pastHour = await pastHourResponse.json();

		// Preprocess line graph data
		let labels = [];
		let values = [];
		for (let i = 0; i < pastHour.length; i++) {
			labels.push(new Date(pastHour[i][0]));
			values.push(pastHour[i][1]);
		}

		data = {
			labels: labels,
			datasets: [
				{
				label: 'Temperature (º)',
				fill: false,
				lineTension: 0.1,
				backgroundColor: 'rgba(51, 153,255, .3)',
				borderColor: 'rgb(0, 76, 153)',
				borderDash: [],
				borderDashOffset: 0.0,
				data: values,
				}
			],
		};
	});

</script>

<main>
	<h1>envsens</h1>
	<h2>Summary statistics for environment sensors</h2>
	<p>Current temperature: {currentTemp} </p>
</main>

<Line {data} options={lineOptions} />

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #0d7d13;
		text-transform: uppercase;
		font-size: 10vw;
		font-weight: bold;
		margin: 0 0;
	}

	h2 {
		color: #034453;
		font-size: 5vw;
		font-weight: bold;
		margin: 0 0;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>