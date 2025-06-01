<script lang="ts">
	import type { PageProps } from "./$types";
	import { setNoteState } from "$lib/state/note.svelte";
	import MakeNote from "$lib/ui/MakeNote.svelte";
	import Layout from "$lib/ui/Masonry.svelte";
	let { data }: PageProps = $props();
	setNoteState(data.data);
</script>

<MakeNote />
<Layout />
