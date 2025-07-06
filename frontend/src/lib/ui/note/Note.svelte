<script lang="ts">
	import NoteBase from "./NoteBase.svelte";
	import { getNoteState } from "$lib/state/note.svelte";
	import { ArchiveIcon, Trash2Icon } from "@lucide/svelte";
	import handler from "$lib/utils/handler";
	let { masonry, id } = $props();

	const noteState = getNoteState();
	let noteSnapshot = $state.snapshot(noteState.findById(id));

	const onClose = handler(async () => {
		if (noteSnapshot) {
			const res = await noteState.update(noteSnapshot);
			if (res && res.data) {
				noteSnapshot = res.data;
				masonry();
			}
		}
	});

	const archive = handler(async (event: MouseEvent) => {
		event.stopPropagation();
		await noteState.archive(id);
	});

	const trash = handler(async (event: MouseEvent) => {
		event.stopPropagation();
		await noteState.trash(id);
	});
</script>

<NoteBase {id} {onClose}>
	{#snippet options()}
		<button onclick={archive}>
			<ArchiveIcon color="#cdd6f4" />
		</button>
		<button onclick={trash}>
			<Trash2Icon color="#cdd6f4" />
		</button>
	{/snippet}
</NoteBase>
