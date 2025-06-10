<script lang="ts">
	import Button from "$lib/components/Button.svelte";
	import Field from "$lib/components/Field.svelte";
</script>

<div class="profile">
	<div class="form">
		<label for="" class="label">Username</label>
		<Field />
		<label for="" class="label">Email</label>
		<Field />
	</div>
	<Button class="button">Save</Button>
</div>

<style>
	.profile {
		display: flex;
		flex-direction: column;
		gap: 10px;
		border: 1px solid #313244;
		border-radius: 8px;
		justify-content: center;
		align-items: center;
		padding: 20px;

		.form {
			display: flex;
			width: 100%;
			flex-direction: column;
			gap: 10px;

			.label {
				color: #a6adc8;
				text-align: left;
				padding: 2px;
			}
		}

		:global(.button) {
			align-self: end;
		}
	}
</style>
