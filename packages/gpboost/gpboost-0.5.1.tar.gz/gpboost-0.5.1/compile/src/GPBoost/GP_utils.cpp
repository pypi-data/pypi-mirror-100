/*!
* This file is part of GPBoost a C++ library for combining
*	boosting with Gaussian process and mixed effects models
*
* Copyright (c) 2020 Fabio Sigrist. All rights reserved.
*
* Licensed under the Apache License Version 2.0. See LICENSE file in the project root for license information.
*/
#include <GPBoost/GP_utils.h>
#include <mutex>
#include <cmath>

namespace GPBoost {

	void DetermineUniqueDuplicateCoords(const den_mat_t& coords,
		data_size_t num_data,
		std::vector<int>& uniques,
		std::vector<int>& unique_idx) {
		uniques = std::vector<int>();
		unique_idx = std::vector<int>();
		uniques.push_back(0);
		unique_idx.push_back(0);
		for (int i = 1; i < num_data; ++i) {//identify duplicates in coordinates
			bool is_duplicate = false;
			//for (const auto& j : uniques) {
			for (int j = 0; j < (int)uniques.size(); ++j) {
				if ((coords.row(uniques[j]) - coords.row(i)).norm() == 0.) {
					unique_idx.push_back(j);
					is_duplicate = true;
					break;
				}
			}
			if (!is_duplicate) {
				unique_idx.push_back((int)uniques.size());
				uniques.push_back(i);
			}
		}
	}

	void CalculateDistances(const den_mat_t& coords1,
		const den_mat_t& coords2,
		bool only_one_set_of_coords,
		den_mat_t& dist) {
		dist = den_mat_t(coords2.rows(), coords1.rows());
		dist.setZero();
#pragma omp parallel for schedule(static)
		for (int i = 0; i < coords2.rows(); ++i) {
			int first_j = 0;
			if (only_one_set_of_coords) {
				dist(i, i) = 0.;
				first_j = i + 1;
			}
			for (int j = first_j; j < coords1.rows(); ++j) {
				dist(i, j) = (coords2.row(i) - coords1.row(j)).lpNorm<2>();
			}
		}
		if (only_one_set_of_coords) {
			dist.triangularView<Eigen::StrictlyLower>() = dist.triangularView<Eigen::StrictlyUpper>().transpose();
		}
	}

	void CalculateDistances(const den_mat_t& coords1,
		const den_mat_t& coords2,
		bool only_one_set_of_coords,
		double,
		den_mat_t& dist) {
		CalculateDistances(coords1, coords2, only_one_set_of_coords, dist);
	}

	void CalculateDistances(const den_mat_t& coords1,
		const den_mat_t& coords2,
		bool only_one_set_of_coords,
		sp_mat_t& dist) {
		std::vector<Triplet_t> triplets;
		int n_max_entry;
		if (only_one_set_of_coords) {
			n_max_entry = (int)(coords1.rows() - 1) * (int)coords2.rows();
		}
		else {
			n_max_entry = (int)coords1.rows() * (int)coords2.rows();
		}
		triplets.reserve(n_max_entry);
#pragma omp parallel for schedule(static)
		for (int i = 0; i < coords1.rows(); ++i) {
			int first_j = 0;
			if (only_one_set_of_coords) {
#pragma omp critical
				{
					triplets.emplace_back(i, i, 0.);
				}
				first_j = i + 1;
			}
			for (int j = first_j; j < coords2.rows(); ++j) {
				double dist_i_j = (coords1.row(i) - coords2.row(j)).lpNorm<2>();
#pragma omp critical
				{
					triplets.emplace_back(i, j, dist_i_j);
					if (only_one_set_of_coords) {
						triplets.emplace_back(j, i, dist_i_j);
					}
				}
			}
		}
		dist = sp_mat_t(coords2.rows(), coords1.rows());
		dist.setFromTriplets(triplets.begin(), triplets.end());
	}

	void CalculateDistances(const den_mat_t& coords1,
		const den_mat_t& coords2,
		bool only_one_set_of_coords,
		double taper_range,
		sp_mat_t& dist) {
		std::vector<Triplet_t> triplets;
		int n_max_entry;
		if (only_one_set_of_coords) {
			n_max_entry = (int)(coords1.rows() - 1) * (int)coords2.rows();
		}
		else {
			n_max_entry = (int)coords1.rows() * (int)coords2.rows();
		}
		triplets.reserve(n_max_entry);
#pragma omp parallel for schedule(static)
		for (int i = 0; i < coords1.rows(); ++i) {
#pragma omp critical
			{
				triplets.emplace_back(i, i, 0.);
			}
			for (int j = i + 1; j < coords2.rows(); ++j) {
				double dist_i_j = (coords1.row(i) - coords2.row(j)).lpNorm<2>();
				if (dist_i_j < taper_range) {
#pragma omp critical
					{
						triplets.emplace_back(i, j, dist_i_j);
						if (only_one_set_of_coords) {
							triplets.emplace_back(j, i, dist_i_j);
						}
					}
				}
			}
		}
		dist = sp_mat_t(coords2.rows(), coords1.rows());
		dist.setFromTriplets(triplets.begin(), triplets.end());
	}

}  // namespace GPBoost
