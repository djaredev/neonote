<script lang="ts">
	import type { PageProps } from "./$types";
	import { setNoteState } from "$lib/state/note.svelte";
	import Layout from "$lib/ui/Masonry.svelte";
	import ArchivedNote from "$lib/ui/note/ArchivedNote.svelte";
	import { getArchivedNotes } from "@neonote/sdk";
	let { data }: PageProps = $props();
	setNoteState(data.data);
</script>

<Layout getData={getArchivedNotes} NoteType={ArchivedNote} />
