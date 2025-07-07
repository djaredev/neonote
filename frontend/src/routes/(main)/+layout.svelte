<script>
	import Sidebar from "$lib/ui/Sidebar.svelte";
	import Header from "$lib/ui/Header.svelte";
	import { setNoteState } from "$lib/state/note.svelte";
	import Notify from "$lib/components/Notify.svelte";

	let { children } = $props();

	let isOpen = $state(false);

	setNoteState([]);
</script>

<Notify />
<Sidebar bind:isOpen />
<div class="main">
	<Header bind:isOpen />
	<div class="content" id="content">
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
