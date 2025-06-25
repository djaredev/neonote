<script lang="ts">
	import type { PageProps } from "./$types";
	import { setNoteState } from "$lib/state/note.svelte";
	import Layout from "$lib/ui/Masonry.svelte";
	import TrashedNote from "$lib/ui/note/TrashedNote.svelte";
	import { getTrashedNotes } from "@neonote/sdk";
	let { data }: PageProps = $props();
	setNoteState(data.data);
</script>

<Layout getData={getTrashedNotes} NoteType={TrashedNote} />
