<script lang="ts">
	import "./Sidebar.svelte";
	import Sidebar from "./Sidebar.svelte";
	import Notebar from "./Notebar.svelte";
	import Note from "./Note.svelte";
	import Layout from "./Masonry.svelte";
</script>

<header></header>

<div class="container">
	<Sidebar />
	<div class="content">
		<Notebar />
		<Layout>
			{#snippet notes(masonry: void)}
				{#each Array(20) as i}
					<Note {masonry} num={i} />
				{/each}
			{/snippet}
		</Layout>
	</div>
</div>

<style>
	header {
		height: 80px;
		background: aqua;
	}

	.container {
		display: flex;
		flex: 1;
		overflow-y: auto;
		/* overflow: hidden; */
	}

	.content {
		display: flex;
		flex-direction: column;
		flex: 1;
		overflow-y: auto;
		padding-left: 60px;
		gap: 10px;
	}
</style>
