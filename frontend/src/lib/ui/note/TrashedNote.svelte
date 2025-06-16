<script lang="ts">
	import NoteBase from "./NoteBase.svelte";
	import { getNoteState } from "$lib/state/note.svelte";
	import { type NotePublic } from "@neonote/sdk";
	import { FileUpIcon, FileXIcon } from "@lucide/svelte";
	let { masonry, id } = $props();

	const noteState = getNoteState();

	function onClose() {
		console.log("Close modal..");
		masonry();
	}

	function restore(event: MouseEvent) {
		event.stopPropagation();
		noteState.restore(id);
	}

	function remove(event: MouseEvent) {
		event.stopPropagation();
		noteState.delete(id);
	}
</script>

<NoteBase {id} {onClose}>
	{#snippet view(note: NotePublic)}
		<div class="note-title" contenteditable="false" bind:innerText={note.title}></div>
		<div class="note-body" contenteditable="false" bind:innerText={note.content}></div>
	{/snippet}
	{#snippet options()}
		<button onclick={restore}>
			<FileUpIcon color="#cdd6f4" />
		</button>
		<button onclick={remove}>
			<FileXIcon color="#cdd6f4" />
		</button>
	{/snippet}
</NoteBase>
