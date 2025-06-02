<script lang="ts">
	import type { PageProps } from "./$types";
	import { setNoteState } from "$lib/state/note.svelte";
	import Layout from "$lib/ui/Masonry.svelte";
	import ArchivedNote from "$lib/ui/note/ArchivedNote.svelte";
	let { data }: PageProps = $props();
	let layout;
	const noteState = setNoteState(data.data);
	const notes = $derived(noteState.getAll());
</script>

<Layout bind:this={layout}>
	{#each notes as note (note.id)}
		<ArchivedNote masonry={layout.masonry} id={note.id} />
	{/each}
</Layout>
