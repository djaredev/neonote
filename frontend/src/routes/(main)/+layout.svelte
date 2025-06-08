<script>
	import Sidebar from "$lib/ui/Sidebar.svelte";
	import Header from "$lib/ui/Header.svelte";

	let { children } = $props();

	let isOpen = $state(false);
</script>

<Sidebar bind:isOpen />
<div class="main">
	<Header bind:isOpen />
	<div class="content">
		{@render children()}
	</div>
</div>

<style>
	.content {
		display: flex;
		width: 100%;
		flex: 1;
		overflow-y: auto;
		gap: 10px;
		justify-content: center;
		container: content / inline-size;
	}

	.main {
		display: flex;
		flex-direction: column;
		flex: 1;
		gap: 10px;
	}
</style>
