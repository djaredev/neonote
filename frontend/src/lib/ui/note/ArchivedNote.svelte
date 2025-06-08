<script lang="ts">
	import NoteBase from "./NoteBase.svelte";
	import { getNoteState } from "$lib/state/note.svelte";
	import { ArchiveRestoreIcon, Trash2Icon } from "@lucide/svelte";
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

	function unArchive(event: MouseEvent) {
		event.stopPropagation();
		noteState.unArchive(id);
	}

	function trash(event: MouseEvent) {
		event.stopPropagation();
		noteState.trash(id);
	}
</script>

<NoteBase {id} {onClose}>
	{#snippet options()}
		<button onclick={unArchive}>
			<ArchiveRestoreIcon color="#cdd6f4" />
		</button>
		<button onclick={trash}>
			<Trash2Icon color="#cdd6f4" />
		</button>
	{/snippet}
</NoteBase>
