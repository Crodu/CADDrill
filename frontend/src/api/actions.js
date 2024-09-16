import api from "./api";

const getAllPlans = async () => {
  try {
    const response = await api.get('/plans/');
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

const startMotorCalibration = async () => {
  try {
    const response = await api.get('/calibrateMotor');
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

const getConfig = async () => {
  try {
    const response = await api.get('/config/');
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

const updateConfig = async (configData) => {
  try {
    const response = await api.post('/config/', configData);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

const addPlan = async (planData, file) => {
  try {
    const formData = new FormData();
    // formData.append('data', JSON.stringify(planData));
    formData.append('name', planData.name);
    formData.append('hole_diameter', planData.hole_diameter);
    formData.append('file', file);

    const response = await api.post('/plans/add', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error(error);
  }
};

const runPlan = async (planId) => {
  try {
    const response = await api.get(`/plans/run/${planId}`);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export { getAllPlans, addPlan, getConfig, updateConfig, runPlan, startMotorCalibration };

// export default getAllPlans;