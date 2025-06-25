<script lang="ts">
	import type { PageProps } from "./$types";
	import { onDestroy } from "svelte";
	import { getNoteState } from "$lib/state/note.svelte";
	import Layout from "$lib/ui/Masonry.svelte";

	let { data }: PageProps = $props();
	const noteState = getNoteState();
	noteState.set(data.data);

	onDestroy(() => {
		noteState.set([]);
	});
</script>

<Layout />
