import yaml
from unittest import mock
import mlagents.trainers.tests.mock_brain as mb
from mlagents.trainers.rl_trainer import RLTrainer
from mlagents.trainers.tests.test_buffer import construct_fake_buffer


def dummy_config():
    return yaml.safe_load(
        """
        summary_path: "test/"
        summary_freq: 1000
        reward_signals:
          extrinsic:
            strength: 1.0
            gamma: 0.99
        """
    )


def create_mock_brain():
    mock_brain = mb.create_mock_brainparams(
        vector_action_space_type="continuous",
        vector_action_space_size=[2],
        vector_observation_space_size=8,
        number_visual_observations=1,
    )
    return mock_brain


# Add concrete implementations of abstract methods
class FakeTrainer(RLTrainer):
    def get_policy(self, name_behavior_id):
        return mock.Mock()

    def _is_ready_update(self):
        return True

    def _update_policy(self):
        pass

    def add_policy(self):
        pass

    def create_policy(self):
        return mock.Mock()

    def _process_trajectory(self, trajectory):
        super()._process_trajectory(trajectory)


def create_rl_trainer():
    mock_brainparams = create_mock_brain()
    trainer = FakeTrainer(mock_brainparams, dummy_config(), True, 0)
    return trainer


def test_rl_trainer():
    trainer = create_rl_trainer()
    agent_id = "0"
    trainer.collected_rewards["extrinsic"] = {agent_id: 3}
    # Test end episode
    trainer.end_episode()
    for rewards in trainer.collected_rewards.values():
        for agent_id in rewards:
            assert rewards[agent_id] == 0


def test_clear_update_buffer():
    trainer = create_rl_trainer()
    trainer.update_buffer = construct_fake_buffer(0)
    trainer.clear_update_buffer()
    for _, arr in trainer.update_buffer.items():
        assert len(arr) == 0
