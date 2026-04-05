import { useQuery } from '@tanstack/react-query'
import { get } from '../api/client'

export function useCourses() {
    return useQuery({
        queryKey: ['courses'],
        queryFn: () => get('/courses')
    })
}