<script lang="ts">
	import type { PageProps } from "./$types";
	import { setNoteState } from "$lib/state/note.svelte";
	import MakeNote from "$lib/ui/MakeNote.svelte";
	import Layout from "$lib/ui/Masonry.svelte";
	import Note from "$lib/ui/note/Note.svelte";

	let { data }: PageProps = $props();
	let layout;
	const noteState = setNoteState(data.data);
	const notes = $derived(noteState.getAll());
</script>

<MakeNote />
<Layout bind:this={layout}>
	{#each notes as note (note.id)}
		<Note masonry={layout.masonry} id={note.id} />
	{/each}
</Layout>
