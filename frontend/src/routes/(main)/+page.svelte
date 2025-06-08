<script lang="ts">
	import type { PageProps } from "./$types";
	import { setNoteState } from "$lib/state/note.svelte";
	import MakeNote from "$lib/ui/MakeNote.svelte";
	import Layout from "$lib/ui/Masonry.svelte";
	import Note from "$lib/ui/note/Note.svelte";
	import LazyLoading from "$lib/ui/LazyLoading.svelte";
	import { getNotes } from "@neonote/sdk";

	let { data }: PageProps = $props();
	let layout: Layout;
	const noteState = setNoteState(data.data);
	let length = noteState.notes.length;
	let count = $state(-10);
	let isLoadingBottom = false;
	let isLoadingTop = false;

	async function loadMore() {
		if (isLoadingBottom) return;
		isLoadingBottom = true;
		const data = await getNotes({
			query: {
				offset: length
			}
		});
		if (data.data && data.data.notes.length > 0) {
			if (noteState.notes.length + data.data.notes.length >= 100) {
				noteState.notes.splice(0, 10);
				layout.waitForTransitions().then(() => {
					noteState.notes.push(...data.data.notes);
					length += data.data.notes.length;
					isLoadingBottom = false;
				});
				count += 10;
			} else {
				noteState.notes.push(...data.data.notes);
				length += data.data.notes.length;
				isLoadingBottom = false;
			}
		}
	}

	async function loadPrevious() {
		if (isLoadingTop) return;
		isLoadingTop = true;
		const content = document.getElementById("content");
		if (!content) return;
		const previousScrollHeight = content.scrollHeight;
		const previousScrollTop = content.scrollTop;
		const data = await getNotes({
			query: {
				offset: count
			}
		});
		if (data.data && data.data.notes.length > 0) {
			noteState.notes.unshift(...data.data.notes);
			layout.waitForTransitions().then(() => {
				const newScrollHeight = content.scrollHeight;
				const deltaHeight = newScrollHeight - previousScrollHeight;
				content.scrollTop = previousScrollTop + deltaHeight;
				if (noteState.notes.length >= 100) {
					noteState.notes.splice(noteState.notes.length - 10, 10);
					length -= 10;
				}
				count -= data.data.notes.length;
			});
		}
		isLoadingTop = false;
	}
</script>

<MakeNote />
<Layout bind:this={layout}>
	{#if count >= 0}
		<LazyLoading loadData={loadPrevious} />
	{/if}
	{#each noteState.notes as note (note.id)}
		<Note masonry={layout.masonry} id={note.id} />
	{/each}
	<LazyLoading loadData={loadMore} />
</Layout>
