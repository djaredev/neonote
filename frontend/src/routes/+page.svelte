<script lang="ts">
	import "./Sidebar.svelte";
	import Sidebar from "./Sidebar.svelte";
	import Notebar from "./Notebar.svelte";
	import Note from "./Note.svelte";
	import Layout from "./Masonry.svelte";
	import { notes as state } from "$lib/state/note.svelte";
</script>

<header></header>

<div class="container">
	<Sidebar />
	<div class="content">
		<Notebar />
		<Layout></Layout>
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

	/* .overlay { */
	/* 	position: fixed; */
	/* 	width: 100%; */
	/* 	height: 100vh; */
	/* 	background-color: rgba(0, 0, 0, 0.5); */
	/* 	opacity: 0; */
	/* 	pointer-events: none; */
	/* 	transition: all 0.05s ease; */
	/* } */
</style>
