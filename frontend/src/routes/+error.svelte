<script lang="ts">
	import { page } from "$app/state";
	import { CircleXIcon } from "@lucide/svelte";
</script>

<div class="container">
	<div class="error">
		<CircleXIcon size={50} />
		<h1>{page.error?.message}</h1>
	</div>
</div>

<style>
	* {
		box-sizing: border-box;
	}
	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		flex: 1;
		color: #f38ba8;
		padding: 20px;
	}
	.error {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 20px;
		width: 600px;
		padding: 20px;
		border: 1px solid #313244;
		border-radius: 10px;
		box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
		overflow: hidden;
		@media (width <= 600px) {
			& {
				flex-direction: column;
				width: 100%;
				height: auto;
			}
		}
	}
</style>
