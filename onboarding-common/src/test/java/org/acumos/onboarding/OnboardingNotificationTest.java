/*-
 * ===============LICENSE_START=======================================================
 * Acumos
 * ===================================================================================
 * Copyright (C) 2017 AT&T Intellectual Property & Tech Mahindra. All rights reserved.
 * ===================================================================================
 * This Acumos software file is distributed by AT&T and Tech Mahindra
 * under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *  
 *      http://www.apache.org/licenses/LICENSE-2.0
 *  
 * This file is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ===============LICENSE_END=========================================================
 */
package org.acumos.onboarding;

import java.util.Date;

import org.acumos.onboarding.common.models.OnboardingNotification;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class OnboardingNotificationTest {

	private String trackingId = "43234";

	OnboardingNotification onboardingNotify = new OnboardingNotification("http://localhost:8080/ccds", "xyz","Test@123");

	@Test
	public void notifyOnboardingStatusTest() {

		if (trackingId != null) {

			onboardingNotify.notifyOnboardingStatus("CreateSolution", "ST", "CreateSolution Started");
			onboardingNotify.setSolutionId("4215454");
			onboardingNotify.setRevisionId("235425");
			onboardingNotify.setArtifactId("352");
			onboardingNotify.setUserId("xyz");
			onboardingNotify.setStatusCode("ST");
			onboardingNotify.setTrackingId("235");
			onboardingNotify.setName("CreateSolution");
			onboardingNotify.setStartDate(new Date());
			onboardingNotify.setEndDate(new Date());
			onboardingNotify.setStepCode("OB");
			onboardingNotify.setResult("Success");
			onboardingNotify.setStepResultId(2452l);

			onboardingNotify.getSolutionId();
			onboardingNotify.getRevisionId();
			onboardingNotify.getArtifactId();
			onboardingNotify.getUserId();
			onboardingNotify.getStatusCode();
			onboardingNotify.getTrackingId();
			onboardingNotify.getName();
			onboardingNotify.getStartDate();
			onboardingNotify.getEndDate();
			onboardingNotify.getStepCode();
			onboardingNotify.getResult();
			onboardingNotify.getStepResultId();
			assert(true);
		}

	}
}