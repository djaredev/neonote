<script lang="ts">
	import NoteBase from "./NoteBase.svelte";
	import trashSVG from "$lib/icons/trash.svg";
	import { getNoteState } from "$lib/state/note.svelte";
	import { type NotePublic } from "@neonote/sdk";
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
</script>

<NoteBase {id} {onClose}>
	{#snippet view(note: NotePublic)}
		<div class="note-title" contenteditable="false" bind:innerText={note.title}></div>
		<div class="note-body" contenteditable="false" bind:innerText={note.content}></div>
	{/snippet}
	{#snippet options()}
		<button onclick={restore}>
			<img src={trashSVG} alt="" />
		</button>
	{/snippet}
</NoteBase>
