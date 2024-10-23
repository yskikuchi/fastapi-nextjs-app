import { getCars } from '@/api/car';
import { Car } from '@/types/car';
import { useEffect, useState } from 'react';

export const useFetchCars = () => {
  const [cars, setCars] = useState<Car[]>([]);
  const [selectedCar, setSelectedCar] = useState<Car>();

  useEffect(() => {
    const fetchCars = async () => {
      const response = await getCars();
      setCars(response);
      setSelectedCar(response[0]);
    };
    fetchCars();
  }, []);

  return { cars, selectedCar, setSelectedCar };
};
