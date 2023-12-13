export interface IFormatResponse<T> {
    success: boolean;
    status: number;
    message: string;
    data: T;
}
