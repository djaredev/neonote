<script>
	import Sidebar from "$lib/ui/Sidebar.svelte";
	import Header from "$lib/ui/Header.svelte";

	let { children } = $props();
</script>

<Header />

<div class="container">
	<Sidebar />
	<div class="content">
		{@render children()}
	</div>
</div>

<style>
	.container {
		display: flex;
		flex: 1;
		overflow-y: auto;
		/* overflow: hidden; */
	}

	.content {
		display: flex;
		flex-direction: column;
		flex: 1;
		overflow-y: auto;
		padding-left: 60px;
		gap: 10px;
	}
</style>
