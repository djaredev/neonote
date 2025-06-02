<script lang="ts">
	import type { PageProps } from "./$types";
	import { setNoteState } from "$lib/state/note.svelte";
	import Layout from "$lib/ui/Masonry.svelte";
	import TrashedNote from "$lib/ui/note/TrashedNote.svelte";
	let { data }: PageProps = $props();
	let layout;
	const noteState = setNoteState(data.data);
	const notes = $derived(noteState.getAll());
</script>

<Layout bind:this={layout}>
	{#each notes as note (note.id)}
		<TrashedNote masonry={layout.masonry} id={note.id} />
	{/each}
</Layout>
