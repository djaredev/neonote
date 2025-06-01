<script lang="ts">
	import type { PageProps } from "./$types";
	import MakeNote from "$lib/ui/MakeNote.svelte";
	let { data }: PageProps = $props();
</script>

<MakeNote />

<style>
</style>
