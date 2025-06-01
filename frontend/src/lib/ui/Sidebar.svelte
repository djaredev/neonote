<script lang="ts">
	import note from "$lib/icons/note.svg";
	import archive from "$lib/icons/archive.svg";
	import trash from "$lib/icons/trash.svg";
</script>

<nav class="sidebar">
	<a href="#" class="active" title="Menu">
		<img src={note} alt="Icono" width="24" height="24" />
		<span>Notes</span>
	</a>
	<a href="#" title="Inicio">
		<img src={archive} alt="Icono" width="24" height="24" />
		<span>Archive</span>
	</a>
	<a href="#" title="Configuración">
		<img src={trash} alt="Icono" width="24" height="24" />
		<span>Trash</span>
	</a>
</nav>

<style>
	.sidebar {
		width: 60px;
		background-color: #11111b;
		padding: 60px 0;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		transition: width 0.3s ease;
		overflow: hidden;
		/* position: sticky; */
		top: 0;
		left: 0;
		bottom: 0;
		z-index: 10;
	}

	.sidebar:hover {
		width: 200px;
	}

	.sidebar a {
		color: #cdd6f4;
		text-decoration: none;
		margin-bottom: 20px;
		font-size: 24px;
		display: flex;
		align-items: center;
		width: 100%;
		padding: 10px 18px;
		transition: background-color 0.3s ease;
		white-space: nowrap;
	}

	.sidebar a:hover,
	.sidebar a.active {
		background-color: #181825;
	}

	.sidebar a span {
		margin-left: 10px;
		display: none;
		font-size: 16px;
	}

	.sidebar:hover a span {
		display: inline;
	}

	.main-content {
		flex-grow: 1;
		margin-left: 60px;
		transition: margin-left 0.3s ease;
		overflow-y: auto;
		height: 100%;
	}

	.sidebar:hover + .main-content {
		margin-left: 240px;
	}

	.header {
		background-color: #11111b;
		border-bottom: 1px solid #313244;
		display: flex;
		justify-content: flex-end;
		position: fixed;
		height: 60px;
		top: 0;
		right: 0;
		left: 0px;
		z-index: 1000;
		transition: left 0.3s ease;
	}

	.sidebar:hover ~ .main-content .header {
		left: 240px;
	}

	.dropdown {
		position: relative;
		display: inline-block;
	}

	.dropbtn {
		background-color: #11111b;
		margin: 15px;
		margin-right: 20px;
		color: white;
		font-size: 16px;
		border: none;
		cursor: pointer;
	}

	.dropdown-content {
		display: none;
		position: absolute;
		right: 0;
		background-color: #f9f9f9;
		min-width: 160px;
		box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
		z-index: 1;
	}

	.dropdown-content a {
		color: black;
		padding: 12px 16px;
		text-decoration: none;
		display: block;
	}

	.dropdown-content a:hover {
		background-color: #f1f1f1;
	}

	.dropdown:hover .dropdown-content {
		display: block;
	}

	.dropdown:hover .dropbtn {
		background-color: #181825;
	}

	.content {
		padding: 80px 20px 20px;
	}

	.bar-container {
		display: flex;
		justify-content: center;
		margin-bottom: 20px;
		margin-top: 50px;
	}
</style>
