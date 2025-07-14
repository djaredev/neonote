<script>
	import "../app.css";
	import neonote from "$lib/icons/neonote.svg";

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={neonote} type="image/svg+xml" />
</svelte:head>

{@render children()}
