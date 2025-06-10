<script lang="ts">
	import Button from "$lib/components/Button.svelte";
	import Field from "$lib/components/Field.svelte";
</script>

<div class="security">
	<div class="title">Change password</div>
	<label for="" class="label">Current password</label>
	<Field />
	<label for="" class="label">New password</label>
	<Field />
	<label for="" class="label">Confirm new password</label>
	<Field />
	<Button class="button">Update password</Button>
</div>

<style>
	.security {
		display: flex;
		flex-direction: column;
		gap: 10px;
		border: 1px solid #313244;
		border-radius: 8px;
		padding: 20px;

		.title {
			color: #a6adc8;
			font-size: 24px;
			font-weight: bold;
		}

		.label {
			color: #a6adc8;
			text-align: left;
			padding: 2px;
		}

		:global(.button) {
			align-self: end;
		}
	}
</style>
