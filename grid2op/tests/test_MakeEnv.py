# Copyright (c) 2019-2020, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of Grid2Op, Grid2Op a testbed platform to model sequential decision making in power systems.

import os
import sys
import unittest
import warnings
import time
import numpy as np
import pdb

from grid2op.tests.helper_path_test import PATH_CHRONICS_Make2, PATH_DATA_TEST
from grid2op.tests.helper_path_test import EXAMPLE_CHRONICSPATH, EXAMPLE_CASEFILE
from grid2op.tests.helper_data_test import case14_redisp_TH_LIM, case14_test_TH_LIM, case14_real_TH_LIM

from grid2op.Exceptions import *
from grid2op.MakeEnv import make_from_dataset_path
from grid2op.MakeEnv.get_default_aux import _get_default_aux
from grid2op.MakeEnv import make
from grid2op.Backend import PandaPowerBackend
from grid2op.Parameters import Parameters
from grid2op.Chronics import Multifolder, ChangeNothing
from grid2op.Chronics import GridStateFromFile, GridStateFromFileWithForecasts
from grid2op.Action import BaseAction, TopologyAction, TopologyAndDispatchAction, VoltageOnlyAction
from grid2op.Observation import CompleteObservation
from grid2op.Reward import FlatReward, L2RPNReward, RedispReward
from grid2op.Rules import AlwaysLegal, DefaultRules
from grid2op.VoltageControler import ControlVoltageFromFile
from grid2op.Opponent import BaseOpponent

# TODO make a test that the defaults are correct for all environment below
# (eg that the env.chronics_handler has
# by default the type given in the "make" function,
# that the backend if of the proper type, that the thermal
# limit are properly set up etc.
# basically, test, for all env, all that is defined there:
# if name_env.lower() == "case14_fromfile":
#    default_grid_path = CASE_14_FILE
#    if chronics_path == '':
#        chronics_path = CHRONICS_MLUTIEPISODE
#
#    defaultinstance_chronics_kwargs = {"chronicsClass": Multifolder, "path": chronics_path,
#                                       "gridvalueClass": GridStateFromFileWithForecasts}
#    default_name_converter = NAMES_CHRONICS_TO_BACKEND
#    default_action_class = TopologyAction
#    default_reward_class = L2RPNReward


class TestLoadingPredefinedEnv(unittest.TestCase):
    def test_blank(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = make("blank", test=True,
                       grid_path=EXAMPLE_CASEFILE,
                       chronics_class=ChangeNothing,
                       action_class=TopologyAndDispatchAction)

    def test_case14_fromfile(self):
        self.skipTest("deprecated test")
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = make("rte_case14_fromfile", test=True)
            obs = env.reset()

    def test_case5_example(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = make("rte_case5_example", test=True)
            obs = env.reset()

    def test_case5_redispatch_available(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True) as env:
                obs = env.reset()
                assert env.redispatching_unit_commitment_availble == True

    def test_case5_can_simulate(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True) as env:
                obs = env.reset()
                sim_obs, reward, done, info = obs.simulate(env.action_space())
                assert sim_obs != obs

    def test_case14_redisp(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = make("rte_case14_redisp", test=True)
            obs = env.reset()

    def test_case14redisp_redispatch_available(self):
        with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                with make("rte_case14_redisp", test=True) as env:
                    obs = env.reset()
                    assert env.redispatching_unit_commitment_availble == True

    def test_case14redisp_can_simulate(self):
        with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                with make("rte_case14_redisp", test=True) as env:
                    obs = env.reset()
                    sim_obs, reward, done, info = obs.simulate(env.action_space())
                    assert sim_obs != obs

    def test_case14redisp_test_thermals(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case14_redisp", test=True) as env:
                obs = env.reset()
                assert np.all(env._thermal_limit_a == case14_redisp_TH_LIM)

    def test_case14_realistic(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = make("rte_case14_realistic", test=True)
            obs = env.reset()

    def test_case14realistic_redispatch_available(self):
        with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                with make("rte_case14_realistic", test=True) as env:
                    obs = env.reset()
                    assert env.redispatching_unit_commitment_availble == True

    def test_case14realistic_can_simulate(self):
        with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                with make("rte_case14_realistic", test=True) as env:
                    obs = env.reset()
                    sim_obs, reward, done, info = obs.simulate(env.action_space())
                    assert sim_obs != obs

    def test_case14realistic_test_thermals(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case14_realistic", test=True) as env:
                obs = env.reset()
                assert np.all(env._thermal_limit_a == case14_real_TH_LIM)

    def test_case14_test(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = make("rte_case14_test", test=True)
            obs = env.reset()

    def test_case14test_redispatch_available(self):
        with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                with make("rte_case14_test", test=True) as env:
                    obs = env.reset()
                    assert env.redispatching_unit_commitment_availble == True

    def test_case14test_can_simulate(self):
        with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                with make("rte_case14_test", test=True) as env:
                    obs = env.reset()
                    sim_obs, reward, done, info = obs.simulate(env.action_space())
                    assert sim_obs != obs

    def test_case14test_thermals(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case14_test", test=True) as env:
                obs = env.reset()
                assert np.all(env._thermal_limit_a == case14_test_TH_LIM)


class TestGetDefault(unittest.TestCase):
    def test_give_instance_default(self):
        kwargs = {}
        param = _get_default_aux('param', kwargs, defaultClass=str, defaultClassApp=str,
                                 msg_error="bad stuff", isclass=False)
        assert param == str(), "This should have returned the empty string"

    def test_give_instance_nodefault(self):
        kwargs = {"param": "toto"}
        param = _get_default_aux('param', kwargs, defaultClass=str, defaultClassApp=str,
                                 msg_error="bad stuff", isclass=False)
        assert param == "toto", "This should have returned \"toto\""

    def test_give_class_default(self):
        kwargs = {}
        param = _get_default_aux('param', kwargs, defaultClass=str, defaultClassApp=str,
                                 msg_error="bad stuff", isclass=True)
        assert param == str, "This should have returned the empty string"

    def test_give_class_nodefault(self):
        kwargs = {"param": str}
        param = _get_default_aux('param', kwargs, defaultClass=str, defaultClassApp=str,
                                 msg_error="bad stuff", isclass=True)
        assert param == str, "This should have returned \"toto\""

    def test_use_sentinel_arg_raises(self):
        with self.assertRaises(RuntimeError):
            _get_default_aux('param', {}, str, _sentinel=True)

    def test_class_not_instance_of_defaultClassApp_raises(self):
        with self.assertRaises(EnvError):
            kwargs = {"param": int}
            _get_default_aux('param', kwargs, defaultClassApp=str, isclass=False)

    def test_type_is_instance_raises(self):
        with self.assertRaises(EnvError):
            kwargs = {"param": 0}
            _get_default_aux('param', kwargs, defaultClassApp=int, isclass=True)

    def test_type_not_subtype_of_defaultClassApp_raises(self):
        with self.assertRaises(EnvError):
            kwargs = {"param": str}
            _get_default_aux('param', kwargs, defaultClassApp=int, isclass=True)

    def test_default_instance_and_class_raises(self):
        with self.assertRaises(EnvError):
            _get_default_aux('param', {}, str,
                             defaultClass=str, defaultinstance="strinstance",
                             isclass=False)

    def test_default_instance_with_build_kwargs_raises(self):
        with self.assertRaises(EnvError):
            _get_default_aux('param', {}, str,
                             defaultinstance="strinstance", isclass=False,
                             build_kwargs=['s', 't', 'r'])

    def test_no_default_provided_raises(self):
        with self.assertRaises(EnvError):
            _get_default_aux('param', {}, str,
                             defaultinstance=None, defaultClass=None,
                             isclass=False)

    def test_class_with_provided_build_kwargs_raises(self):
        with self.assertRaises(EnvError):
            _get_default_aux('param', {}, str,
                             defaultClass=str,
                             isclass=True, build_kwargs=['s', 't', 'r'])

    def test_class_with_provided_instance_raises(self):
        with self.assertRaises(EnvError):
            _get_default_aux('param', {}, str,
                             defaultClass=str,
                             defaultinstance="strinstance",
                             isclass=True)


class TestkwargsName(unittest.TestCase):
    def test_param(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, param=Parameters()) as env:
                obs = env.reset()

    def test_backend(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, backend=PandaPowerBackend()) as env:
                obs = env.reset()

    def test_obsclass(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, observation_class=CompleteObservation) as env:
                obs = env.reset()

    def test_gamerules(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, gamerules_class=AlwaysLegal) as env:
                obs = env.reset()

    def test_chronics_path(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, chronics_path=EXAMPLE_CHRONICSPATH) as env:
                obs = env.reset()

    def test_reward_class(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, reward_class=FlatReward) as env:
                obs = env.reset()

    def test_action_class(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, action_class=BaseAction) as env:
                obs = env.reset()

    def test_grid_path(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, grid_path=EXAMPLE_CASEFILE) as env:
                obs = env.reset()

    def test_names_chronics_to_backend(self):
        self.skipTest("deprecated test for now")
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, names_chronics_to_backend={}) as env:
                obs = env.reset()

    def test_data_feeding_kwargs(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            dict_ = {"chronicsClass": Multifolder, "path": EXAMPLE_CHRONICSPATH,
                    "gridvalueClass": GridStateFromFileWithForecasts}
            with make("rte_case5_example", test=True, data_feeding_kwargs=dict_) as env:
                obs = env.reset()

    def test_chronics_class(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, chronics_class=Multifolder) as env:
                pass

    def test_voltagecontroler_class(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, voltagecontroler_class=ControlVoltageFromFile) as env:
                obs = env.reset()

    def test_other_rewards(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, other_rewards={"test": L2RPNReward}) as env:
                obs = env.reset()

    def test_opponent_action_class(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, opponent_action_class=BaseAction) as env:
                obs = env.reset()

    def test_opponent_class(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, opponent_class=BaseOpponent) as env:
                obs = env.reset()

    def test_opponent_init_budget(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make("rte_case5_example", test=True, opponent_init_budget=10) as env:
                obs = env.reset()


class TestMakeFromPathConfig(unittest.TestCase):
    def test_case5_config(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case5_example")
        with make_from_dataset_path(dataset_path) as env:
            # Check config is loaded from config.py
            assert env.rewardClass == L2RPNReward
            assert env.actionClass == TopologyAction
            assert env.observationClass == CompleteObservation
            assert isinstance(env.backend, PandaPowerBackend)
            assert env.legalActClass == DefaultRules
            assert isinstance(env.voltage_controler, ControlVoltageFromFile)
            assert isinstance(env.chronics_handler.real_data, Multifolder)
            assert env.action_space.grid_layout != None
            
    def test_case5_runs(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case5_example")
        with make_from_dataset_path(dataset_path) as env:
            assert env.redispatching_unit_commitment_availble == True
            obs = env.reset()
            sim_obs, reward, done, info = obs.simulate(env.action_space())
            assert sim_obs != obs

    def test_case14_test_config(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case14_test")
        with make_from_dataset_path(dataset_path) as env:
            # Check config is loaded from config.py
            assert env.rewardClass == RedispReward
            assert env.actionClass == TopologyAndDispatchAction
            assert env.observationClass == CompleteObservation
            assert isinstance(env.backend, PandaPowerBackend)
            assert env.legalActClass == DefaultRules
            assert isinstance(env.voltage_controler, ControlVoltageFromFile)
            assert isinstance(env.chronics_handler.real_data, Multifolder)
            assert env.action_space.grid_layout != None
            
    def test_case14_test_runs(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case14_test")
        with make_from_dataset_path(dataset_path) as env:
            assert env.redispatching_unit_commitment_availble == True
            obs = env.reset()
            sim_obs, reward, done, info = obs.simulate(env.action_space())
            assert sim_obs != obs
            assert np.all(env._thermal_limit_a == case14_test_TH_LIM)

    def test_case14_redisp_config(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case14_redisp")
        with make_from_dataset_path(dataset_path) as env:
            # Check config is loaded from config.py
            assert env.rewardClass == RedispReward
            assert env.actionClass == TopologyAndDispatchAction
            assert env.observationClass == CompleteObservation
            assert isinstance(env.backend, PandaPowerBackend)
            assert env.legalActClass == DefaultRules
            assert isinstance(env.voltage_controler, ControlVoltageFromFile)
            assert isinstance(env.chronics_handler.real_data, Multifolder)
            
    def test_case14_redisp_runs(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case14_redisp")
        with make_from_dataset_path(dataset_path) as env:
            assert env.redispatching_unit_commitment_availble == True
            obs = env.reset()
            sim_obs, reward, done, info = obs.simulate(env.action_space())
            assert sim_obs != obs
            assert np.all(env._thermal_limit_a == case14_redisp_TH_LIM)

    def test_l2rpn19_test_config(self):
        self.skipTest("l2rpn has been removed")
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "l2rpn_2019")
        with make_from_dataset_path(dataset_path) as env:
            # Check config is loaded from config.py
            assert env.rewardClass == L2RPNReward
            assert env.actionClass == TopologyAction
            assert env.observationClass == CompleteObservation
            assert isinstance(env.backend, PandaPowerBackend)
            assert env.legalActClass == DefaultRules
            assert isinstance(env.voltage_controler, ControlVoltageFromFile)
            assert isinstance(env.chronics_handler.real_data, Multifolder)
            assert env.action_space.grid_layout != None


class TestMakeFromPathConfigOverride(unittest.TestCase):
    def test_case5_override_reward(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case5_example")
        with make_from_dataset_path(dataset_path, reward_class=FlatReward) as env:
            assert env.rewardClass == FlatReward

    def test_case14_test_override_reward(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case14_test")
        with make_from_dataset_path(dataset_path, reward_class=FlatReward) as env:
            assert env.rewardClass == FlatReward

    def test_l2rpn19_override_reward(self):
        self.skipTest("l2rpn has been removed")
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "l2rpn_2019")
        with make_from_dataset_path(dataset_path, reward_class=FlatReward) as env:
            assert env.rewardClass == FlatReward

    def test_case5_override_action(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case5_example")
        with make_from_dataset_path(dataset_path, action_class=VoltageOnlyAction) as env:
            assert env.actionClass == VoltageOnlyAction

    def test_case14_test_override_action(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case14_test")
        with make_from_dataset_path(dataset_path, action_class=VoltageOnlyAction) as env:
            assert env.actionClass == VoltageOnlyAction

    def test_l2rpn19_override_action(self):
        self.skipTest("l2rpn has been removed")
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "l2rpn_2019")
        with make_from_dataset_path(dataset_path, action_class=VoltageOnlyAction) as env:
            assert env.actionClass == VoltageOnlyAction

    def test_case5_override_chronics(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case5_example")
        with make_from_dataset_path(dataset_path, chronics_class=ChangeNothing) as env:
            assert isinstance(env.chronics_handler.real_data, ChangeNothing)

    def test_case14_test_override_chronics(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case14_test")
        with make_from_dataset_path(dataset_path, chronics_class=ChangeNothing) as env:
            assert isinstance(env.chronics_handler.real_data, ChangeNothing)

    def test_l2rpn19_override_chronics(self):
        self.skipTest("l2rpn has been removed")
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "l2rpn_2019")
        with make_from_dataset_path(dataset_path, chronics_class=ChangeNothing) as env:
            assert isinstance(env.chronics_handler.real_data, ChangeNothing)

    def test_case5_override_feed_kwargs(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case5_example")
        chronics_path = os.path.join(dataset_path, "chronics", "0")
        dfk = {
            "chronicsClass": ChangeNothing,
            "path": chronics_path,
            "gridvalueClass": GridStateFromFile
        }
        with make_from_dataset_path(dataset_path, data_feeding_kwargs=dfk) as env:
            assert isinstance(env.chronics_handler.real_data, ChangeNothing)

    def test_case14_test_override_feed_kwargs(self):
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "rte_case14_test")
        chronics_path = os.path.join(dataset_path, "chronics", "0")
        dfk = {
            "chronicsClass": ChangeNothing,
            "path": chronics_path,
            "gridvalueClass": GridStateFromFile
        }
        with make_from_dataset_path(dataset_path, data_feeding_kwargs=dfk) as env:
            assert isinstance(env.chronics_handler.real_data, ChangeNothing)

    def test_l2rpn19_override_feed_kwargs(self):
        self.skipTest("l2rpn has been removed")
        dataset_path = os.path.join(PATH_CHRONICS_Make2, "l2rpn_2019")
        chronics_path = os.path.join(dataset_path, "chronics", "0000")
        dfk = {
            "chronicsClass": ChangeNothing,
            "path": chronics_path,
            "gridvalueClass": GridStateFromFile
        }
        with make_from_dataset_path(dataset_path, data_feeding_kwargs=dfk) as env:
            assert isinstance(env.chronics_handler.real_data, ChangeNothing)


class TestMakeFromPathParameters(unittest.TestCase):
    def test_case5_some_missing(self):
        dataset_path = os.path.join(PATH_DATA_TEST, "5bus_example_some_missing")
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with make_from_dataset_path(dataset_path) as env:
                assert env.parameters.NB_TIMESTEP_TOPOLOGY_REMODIF == 19


if __name__ == "__main__":
    unittest.main()
