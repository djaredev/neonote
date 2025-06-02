<script lang="ts">
	import NoteBase from "./NoteBase.svelte";
	import archiveSVG from "$lib/icons/archive.svg";
	import trashSVG from "$lib/icons/trash.svg";
	import { getNoteState } from "$lib/state/note.svelte";
	let { masonry, id } = $props();

	const noteState = getNoteState();
	const noteSnapshot = $state.snapshot(noteState.findById(id));

	function onClose() {
		console.log("Close modal..");
		if (noteSnapshot) {
			const res = noteState.update(noteSnapshot);
			console.log(res);
		}
		masonry();
	}

	function archive(event: MouseEvent) {
		event.stopPropagation();
		noteState.archive(id);
	}

	function trash(event: MouseEvent) {
		event.stopPropagation();
		noteState.trash(id);
	}
</script>

<NoteBase {id} {onClose}>
	{#snippet options()}
		<button onclick={archive}>
			<img src={archiveSVG} alt="" />
		</button>
		<button onclick={trash}>
			<img src={trashSVG} alt="" />
		</button>
	{/snippet}
</NoteBase>
